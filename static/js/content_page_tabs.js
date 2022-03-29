$(document).ready(function () {
    $("#tabs a").click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
    $("#users_management_tabs a").click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
    $("#projects_management_tabs a").click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
});