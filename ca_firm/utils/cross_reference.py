import frappe


def create_cross_reference(
	source_doctype, source_name, target_doctype, target_name, relationship_type,
	client=None, linked_head=None, linked_fs_line_item=None, remarks=None, raised_by=None,
):
	"""Log a two-way linkage between a workpaper in one assignment module and a
	workpaper (or Audit Adjustment / Audit Finding) in another, so the impact
	of one team's work on another's is discoverable from either side via
	get_cross_references() or the Cross Module Linkages report -- instead of
	each module silently carrying its own unrelated copy of a figure.
	Idempotent: re-raising the same source/target/relationship combination
	updates the existing entry rather than creating a duplicate."""
	existing = frappe.db.exists(
		"Engagement Cross Reference",
		{
			"source_doctype": source_doctype,
			"source_name": source_name,
			"target_doctype": target_doctype,
			"target_name": target_name,
			"relationship_type": relationship_type,
		},
	)
	if existing:
		doc = frappe.get_doc("Engagement Cross Reference", existing)
	else:
		doc = frappe.new_doc("Engagement Cross Reference")
		doc.source_doctype = source_doctype
		doc.source_name = source_name
		doc.target_doctype = target_doctype
		doc.target_name = target_name
		doc.relationship_type = relationship_type

	if not client:
		client = frappe.db.get_value(source_doctype, source_name, "client")
	doc.client = client
	doc.linked_head = linked_head
	doc.linked_fs_line_item = linked_fs_line_item
	doc.remarks = remarks
	doc.raised_by = raised_by or frappe.db.get_value(
		"Employee", {"user_id": frappe.session.user}, "name"
	)
	if doc.status is None:
		doc.status = "Open"
	if doc.is_new():
		doc.insert(ignore_permissions=True)
	else:
		doc.save(ignore_permissions=True)
	return doc.name


@frappe.whitelist()
def get_cross_references(doctype, name):
	"""Every cross-reference touching this record, whichever side it was
	raised from -- so a doc doesn't need to know in advance whether it was
	the source or the target to show its full linkage picture."""
	as_source = frappe.get_all(
		"Engagement Cross Reference",
		filters={"source_doctype": doctype, "source_name": name},
		fields=["name", "target_doctype", "target_name", "relationship_type",
		        "linked_head", "linked_fs_line_item", "status", "remarks", "raised_by", "creation"],
	)
	for r in as_source:
		r["direction"] = "outgoing"
		r["other_doctype"] = r.pop("target_doctype")
		r["other_name"] = r.pop("target_name")

	as_target = frappe.get_all(
		"Engagement Cross Reference",
		filters={"target_doctype": doctype, "target_name": name},
		fields=["name", "source_doctype", "source_name", "relationship_type",
		        "linked_head", "linked_fs_line_item", "status", "remarks", "raised_by", "creation"],
	)
	for r in as_target:
		r["direction"] = "incoming"
		r["other_doctype"] = r.pop("source_doctype")
		r["other_name"] = r.pop("source_name")

	return sorted(as_source + as_target, key=lambda r: r["creation"], reverse=True)
