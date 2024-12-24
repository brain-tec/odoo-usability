POS Check Deposit
=================

On POS payment method, there is a boolean field named **split_transactions** which has a string **Identify Customer**. When this option is enabled, the payment move lines are split (which is required for the account_check_deposit module) and you must select a Customer on the POS order (which is not really needed for a payment by check).

The goal of this module is to have 2 different options on POS payment method:

* split_transactions (the current field), to split the payment move lines
* identify_customer (a new field), to require the selection of a customer on the POS order

That way, you can configure the **Check** payment method with split_transactions enabled and identify_customer disabled.

WARNING: this module requires a patch on the point_of_sale module. The patch is available in the root directory of the module under the name **odoo-pos_check_deposit.diff**.

Authors
-------

Akretion:

* Alexis de Lattre <alexis.delattre@akretion.com>
