function confirm_product_delete(id) {
    var r = confirm("Rostan o'chirishni hohlasysizmi?");
    if (r == true) {
        window.location.href = "product/delete/" + id + "/"
    }
    else {
        // Do nothing or show a message to the user
        console.log("Delete canceled");
    }
}

