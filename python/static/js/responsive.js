// responsive.js

function updateProductColumns() {
    const productsContainers = document.querySelectorAll('.products-container');
    const windowWidth = window.innerWidth;

    let columns;
    if (windowWidth >= 1200) {
        columns = 4;
    } else if (windowWidth >= 992) {
        columns = 3;
    } else if (windowWidth >= 768) {
        columns = 2;
    } else {
        columns = 1;
    }

    productsContainers.forEach(container => {
        const productCards = container.querySelectorAll('.product-card');
        productCards.forEach(card => {
            card.style.flexBasis = `calc(${100 / columns}% - 20px)`;
        });
    });
}

window.onload = updateProductColumns;
window.onresize = updateProductColumns;
