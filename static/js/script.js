// Fungsi untuk tambah buku
$("#addBookForm").submit(function (e) {
    e.preventDefault();

    let title = $("#input-title").val();
    let author = $("#input-author").val();
    let year = $("#input-year").val();
    let genre = $("#input-genre").val();
    let price = $("#input-price").val();
    let photo = $("#input-photo")[0].files[0];

    let formData = new FormData();
    formData.append('title_give', title);
    formData.append('author_give', author);
    formData.append('year_give', year);
    formData.append('genre_give', genre);
    formData.append('price_give', price);
    formData.append('photo_give', photo);

    $.ajax({
        type: "POST",
        url: "/books/add",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            alert("Book added successfully!");
            location.reload();
        }
    });
});

function delete_book(title) {
    if (confirm(`Are you sure you want to delete the book: ${title}?`)) {
        $.ajax({
            type: "POST",
            url: "/books/delete",
            data: {
                title_give: title
            },
            success: function (response) {
                alert(response['message']);
                location.reload();
            },
            error: function (error) {
                alert('Failed to delete book');
                console.log(error);
            }
        });
    }
}


// Menampilkan modal edit dengan data buku
function show_edit_modal(bookId, title, author, year, genre, price) {
    $('#edit-book-id').val(bookId);
    $('#edit-title').val(title);
    $('#edit-author').val(author);
    $('#edit-year').val(year);
    $('#edit-genre').val(genre);
    $('#edit-price').val(price);
    $('#editBookModal').modal('show');
}


// Fungsi untuk menyimpan perubahan menggunakan AJAX
function edit_book() {
    let bookId = $('#edit-book-id').val();
    let title = $('#edit-title').val();
    let author = $('#edit-author').val();
    let year = $('#edit-year').val();
    let genre = $('#edit-genre').val();
    let price = $('#edit-price').val();

    $.ajax({
        type: "POST",
        url: "/books/edit",
        data: {
            id_give: bookId,
            title_give: title,
            author_give: author,
            year_give: year,
            genre_give: genre,
            price_give: price
        },
        success: function (response) {
            alert(response['message']);
            $('#editBookModal').modal('hide');
            location.reload();
        },
        error: function (error) {
            alert('Failed to edit book');
            console.log(error);
        }
    });
}
