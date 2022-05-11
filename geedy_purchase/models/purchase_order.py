# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import _, api, exceptions, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _purchase_request_confirm_message_content(self, request, request_dict=None):
        self.ensure_one()
        if not request_dict:
            request_dict = {}
        title = _("Order confirmation %s for your Request %s") % (
            self.name,
            request.name,
        )
        message = "<h3>%s</h3><ul>" % title
        message += _(
            "The following requested items from Purchase Request %s "
            "have now been confirmed in Purchase Order %s:"
        ) % (request.name, self.name)

        for line in request_dict.values():
            message += _(
                "<li><b>%s</b>: Ordered quantity %s %s, Planned date %s</li>"
            ) % (
                line["name"],
                line["product_qty"],
                line["product_uom"],
                line["date_planned"],
            )
        message += "</ul>"
        return message

    def _purchase_request_confirm_message(self):
        request_obj = self.env["purchase.request"]
        for po in self:
            requests_dict = {}
            for line in po.order_line:
                for request_line in line.sudo().purchase_request_lines:
                    request_id = request_line.request_id.id
                    if request_id not in requests_dict:
                        requests_dict[request_id] = {}
                    date_planned = "%s" % line.date_planned
                    data = {
                        "name": request_line.name,
                        "product_qty": line.product_qty,
                        "product_uom": line.product_uom.name,
                        "date_planned": date_planned,
                    }
                    requests_dict[request_id][request_line.id] = data
            for request_id in requests_dict:
                request = request_obj.sudo().browse(request_id)
                message = po._purchase_request_confirm_message_content(
                    request, requests_dict[request_id]
                )
                request.message_post(
                    body=message, subtype_id=self.env.ref("mail.mt_comment").id
                )
        return True

    def _purchase_request_line_check(self):
        for po in self:
            for line in po.order_line:
                for request_line in line.purchase_request_lines:
                    if request_line.sudo().purchase_state == "done":
                        raise exceptions.UserError(
                            _("Purchase Request %s has already been completed")
                            % request_line.request_id.name
                        )
        return True

    def button_confirm(self):
        self._purchase_request_line_check()
        res = super(PurchaseOrder, self).button_confirm()
        self._purchase_request_confirm_message()
        return res

    def unlink(self):
        alloc_to_unlink = self.env["purchase.request.allocation"]
        for rec in self:
            for alloc in (
                rec.order_line.mapped("purchase_request_lines")
                .mapped("purchase_request_allocation_ids")
                .filtered(lambda alloc: alloc.purchase_line_id.order_id.id == rec.id)
            ):
                alloc_to_unlink += alloc
        res = super().unlink()
        alloc_to_unlink.unlink()
        return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchase_request_lines = fields.Many2many(
        comodel_name="purchase.request.line",
        relation="purchase_request_purchase_order_line_rel",
        column1="purchase_order_line_id",
        column2="purchase_request_line_id",
        string="Purchase Request Lines",
        readonly=True,
        copy=False,
    )
    purchase_request_allocation_ids = fields.One2many(
        comodel_name="purchase.request.allocation",
        inverse_name="purchase_line_id",
        string="Purchase Request Allocation",
        copy=False,
    )
    discount_type = fields.Selection([
        ('multi', 'Multi Percentage'),
        ('fix', 'Fix Discount')
    ], string='Discount Lines Type', default='multi')
    multi_discount = fields.Char(string='Multi (%) Discount', readonly=True, states={'draft': [('readonly', False)]})
    fix_discount = fields.Float('Fix Discount', copy=False, digits='Fix Discount', default=0.0, readonly=True, states={'draft': [('readonly', False)]})
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)

    @api.onchange('discount_type')
    def _onchange_discount_type(self):
        for line in self:
            line.update({
                'multi_discount': '',
                'fix_discount': 0.0,
                'discount': 0.0,
            })

    @api.depends('product_qty', 'discount_type', 'fix_discount', 'multi_discount', 'discount', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        super(PurchaseOrderLine, self)._compute_amount()
        for line in self:
            if line.discount_type == 'multi' and line.multi_discount:
                vals = line._prepare_compute_all_values()
                persentage = line.multi_discount.split('+')
                disc = 1
                for persent in persentage:
                    persent2 = float(persent)
                    if isinstance(persent2, float):
                        disc = disc - (disc * (persent2/100))
                discount = (1 - disc) * 100
                price = line.price_unit * (1 - discount / 100.0)
                taxes = line.taxes_id.compute_all(price, vals['currency'], vals['quantity'], vals['product'], vals['partner'])
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                    'discount': discount,
                })
            if line.discount_type == 'fix' and line.fix_discount > 0:
                if line.price_unit > 0:
                    discount = (line.fix_discount/line.price_unit) * 100
                else:
                    discount = 0.0
                price = line.price_unit - line.fix_discount
                taxes = line.taxes_id.compute_all(price, vals['currency'], vals['quantity'], vals['product'], vals['partner'])
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                    'discount': discount,
                })

    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move=move)
        res['discount'] = self.discount
        return res

    def action_open_request_line_tree_view(self):
        """
        :return dict: dictionary value for created view
        """
        request_line_ids = []
        for line in self:
            request_line_ids += line.purchase_request_lines.ids

        domain = [("id", "in", request_line_ids)]

        return {
            "name": _("Purchase Request Lines"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.request.line",
            "view_mode": "tree,form",
            "domain": domain,
        }

    def _prepare_stock_moves(self, picking):
        self.ensure_one()
        val = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        all_list = []
        for v in val:
            all_ids = self.env["purchase.request.allocation"].search(
                [("purchase_line_id", "=", v["purchase_line_id"])]
            )
            for all_id in all_ids:
                all_list.append((4, all_id.id))
            v["purchase_request_allocation_ids"] = all_list
        return val

    def update_service_allocations(self, prev_qty_received):
        for rec in self:
            allocation = self.env["purchase.request.allocation"].search(
                [
                    ("purchase_line_id", "=", rec.id),
                    ("purchase_line_id.product_id.type", "=", "service"),
                ]
            )
            if not allocation:
                return
            qty_left = rec.qty_received - prev_qty_received
            for alloc in allocation:
                allocated_product_qty = alloc.allocated_product_qty
                if not qty_left:
                    alloc.purchase_request_line_id._compute_qty()
                    break
                if alloc.open_product_qty <= qty_left:
                    allocated_product_qty += alloc.open_product_qty
                    qty_left -= alloc.open_product_qty
                    alloc._notify_allocation(alloc.open_product_qty)
                else:
                    allocated_product_qty += qty_left
                    alloc._notify_allocation(qty_left)
                    qty_left = 0
                alloc.write({"allocated_product_qty": allocated_product_qty})

                message_data = self._prepare_request_message_data(
                    alloc, alloc.purchase_request_line_id, allocated_product_qty
                )
                message = self._purchase_request_confirm_done_message_content(
                    message_data
                )
                alloc.purchase_request_line_id.request_id.message_post(
                    body=message, subtype_id=self.env.ref("mail.mt_comment").id
                )

                alloc.purchase_request_line_id._compute_qty()
        return True

    @api.model
    def _purchase_request_confirm_done_message_content(self, message_data):
        title = _("Service confirmation for Request %s") % (
            message_data["request_name"]
        )
        message = "<h3>%s</h3>" % title
        message += _(
            "The following requested services from Purchase"
            " Request %s requested by %s "
            "have now been received:"
        ) % (message_data["request_name"], message_data["requestor"])
        message += "<ul>"
        message += _("<li><b>%s</b>: Received quantity %s %s</li>") % (
            message_data["product_name"],
            message_data["product_qty"],
            message_data["product_uom"],
        )
        message += "</ul>"
        return message

    def _prepare_request_message_data(self, alloc, request_line, allocated_qty):
        return {
            "request_name": request_line.request_id.name,
            "product_name": request_line.product_id.name_get()[0][1],
            "product_qty": allocated_qty,
            "product_uom": alloc.product_uom_id.name,
            "requestor": request_line.request_id.requested_by.partner_id.name,
        }

    def write(self, vals):
        #  As services do not generate stock move this tweak is required
        #  to allocate them.
        prev_qty_received = {}
        if vals.get("qty_received", False):
            service_lines = self.filtered(lambda l: l.product_id.type == "service")
            for line in service_lines:
                prev_qty_received[line.id] = line.qty_received
        res = super(PurchaseOrderLine, self).write(vals)
        if prev_qty_received:
            for line in service_lines:
                line.update_service_allocations(prev_qty_received[line.id])
        return res
