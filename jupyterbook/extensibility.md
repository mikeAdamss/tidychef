# Extensibility

One important thing to understand about tidychef is it's designed first and foremost as an _extensible framework_.

Vanilla tidychef is a powerful thing and will allow you to create robust, reliable and repeatable data transformation recipes relatively easily and for many users will be all that's required.

But the world of data is a wide one, and the sheer scope of the "messy" in messy data wider still. Apply that across all of the domains of data and the constantly evolving plethora of formats, schemas and approaches and you end up with a potential scope beyond that of any single tool.

Therefore, tidychef has been consciously designed as a "very unlocked box" so to speak.

- Want to load a new data format into tidychef? It's not that hard and its documented.
- Want to acquire a known data format via a different mechanism (ftp rather than http say, or pulled from your own datastore) ? It's not that hard and its documented.
- Want to create ad-hoc selection filters to support your specific use case? It's not that hard and its documented.
- Want to extend selection classes with methods _that **you specifically** would benefit from_? It's not that hard and its documented.
- Want to create custom validators suitable to your own use case and data domain? It's not that hard and its documented.

The point here is that tidychef was build with the idea that regular users would begin amassing (and possibly even sharing) additional functionality and as such said functionality is easily intermingled, injected and used seemlessly alongside the vanilla tidychef package. 

The vision for tidychef is to be a reliable core for messy data ETL processing, but you can go very far indeed building on that core.