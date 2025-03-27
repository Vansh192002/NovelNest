let allAtags = document.getElementsByTagName("a");

const currentButtonCss = {
    background: "transparent",
    width : "100%"
};

let tagsArray = Array.from(allAtags);

tagsArray.forEach((element) => {
    element.addEventListener("click", () => {
        tagsArray.forEach((el) => {
            el.style.background = "transparent";
        });

        element.style.background = currentButtonCss.background;
    });
});
