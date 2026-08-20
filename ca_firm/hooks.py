from ca_firm import __version__ as app_version  # noqa: F401

app_name = "ca_firm"
app_title = "CA Firm"
app_publisher = "CA Firm"
app_description = "Complete Statutory Audit Management for Chartered Accountancy Firms"
app_email = "jwabdms@gmail.com"
app_license = "MIT"
app_logo_url = "/assets/ca_firm/images/ca-firm-logo.svg"

# Apps screen tile (the grid shown at /apps and in the app switcher)
add_to_apps_screen = [
	{
		"name": "ca_firm",
		"logo": "/assets/ca_firm/images/ca-firm-logo.svg",
		"title": "CA Firm",
		"route": "/app/ca-firm",
	}
]

# Installation
# ------------
after_install = "ca_firm.setup.install.after_install"
after_migrate = "ca_firm.setup.install.after_migrate"

# Includes in <head>
# ------------------
# app_include_css = "/assets/ca_firm/css/ca_firm.css"
# app_include_js = "/assets/ca_firm/js/ca_firm.js"

# Home Pages
# ----------
# role_home_page = {"CA Firm Client": "me"}

# Document Events
# ----------------
# Hook on document methods and events.
#
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 	}
# }

# Fixtures
# --------
# Roles, the Workspace, Dashboards, Kanban Boards and master/reference data are
# created idempotently by ca_firm.setup.install on install and on every migrate,
# instead of static fixtures, so that they can carry real setup logic
# (e.g. skipping creation when a firm has already customised a record).
