Intrastat Product Type
======================

This module is designed for a very special usage scenario: some companies want to handle the delivery of services the same way as they handle the delivery of goods; they want to show the services in the delivery note. So, those companies configure the services with Type = *Consumable*. This works well to have the services on the outgoing pickings, but it is a problem for the intrastat declarations.

This module adds a field *Intrastat Type* on *Consumable* products with 2 possible options: *Product* or *Service*. The intrastat declaration will use this field instead of the native *Type* field.

Credits
=======

Authors
~~~~~~~

* Akretion

Contributors
~~~~~~~~~~~~

* Alexis de Lattre <alexis.delattre@akretion.com>
