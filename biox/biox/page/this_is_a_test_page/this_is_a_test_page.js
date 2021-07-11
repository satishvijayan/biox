frappe.pages['this-is-a-test-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'this is a test page',
		single_column: true
	});
}