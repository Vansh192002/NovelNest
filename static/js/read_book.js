document.addEventListener("DOMContentLoaded", function () {
    updatePageContent(bookId, currentPage)
});

const nextBtn = document.getElementById("next-btn");
const prevBtn = document.getElementById("prev-btn");
const mainPage = document.getElementById("page-content")
const loader = document.getElementById("loader")

let currentPage = 1;
const bookId = prevBtn.getAttribute("data-book-id");
const totalPages = prevBtn.getAttribute("data-total-pages");

const pageCache = {}
pageCache[currentPage] = null


prevBtn.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        updatePageContent(bookId, currentPage);
    }
});

nextBtn.addEventListener("click", () => {
    if (currentPage < totalPages) {
        currentPage++;
        updatePageContent(bookId, currentPage);
    }
});

function updatePageContent(bookId, pageNumber) {


    fetch(`/get_book_page/${bookId}/page/${pageNumber}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load page')
            }
            return response.blob()
        })
        .then(imageBlob => {
            const imageURL = URL.createObjectURL(imageBlob);

            const imgElement = document.createElement("img");
            imgElement.src = imageURL;
            imgElement.alt = `Page  ${pageNumber + 1}`;
            imgElement.classList.add('transition-opacity', 'duration-500', 'ease-in-out', 'object-fit', 'h-146', 'w-full');

            const bookContent = document.getElementById("book-content");
            bookContent.innerHTML = '';
            bookContent.appendChild(imgElement);

            if (mainPage.classList.contains('hidden')) {
                loader.classList.add('hidden')
                mainPage.classList.remove('hidden')
            }

        })

        .catch(error => {
            console.error('Error Fetching page', error);
        });
}