var x = 0;
function myFunction() {
    // document.getElementById('anime_synopsis').classList.add('showSynopsis');
    // document.getElementById('poster').classList.add('hidePoster');
    // document.getElementById('innerItem').classList.add('showCard');
    console.log('works')
    // const ele = document.getElementById("anime_synopsis");
    // const custom_style = {
    //     display: "block",
    // }
    // const ele2 = document.getElementById("poster");
    // const custom_style2 = {
    //     display: "block",
    // }
    // const ele3 = document.getElementById("innerItem");
    // const custom_style3 = {
    //     "background-color": "#8d6572",
    //     "flex-direction": "row",
    //     "width": "500px",
    // }
    if (x == 0) {
        document.getElementById("anime_synopsis").classList.add("showSynopsis");
        document.getElementById("anime_synopsis").classList.remove("anime_synopsis");
        document.getElementById("poster").classList.add("hidePoster");
        document.getElementById("poster").classList.remove("poster");
        document.getElementById("innerItem").classList.add("showCard");
        document.getElementById("innerItem").classList.remove("innerItem");
        x = 1;
    } else {
        document.getElementById("anime_synopsis").classList.remove("showSynopsis");
        document.getElementById("anime_synopsis").classList.add("anime_synopsis");
        document.getElementById("poster").classList.remove("hidePoster");
        document.getElementById("poster").classList.add("poster");
        document.getElementById("innerItem").classList.remove("showCard");
        document.getElementById("innerItem").classList.add("innerItem");
        x = 0;
    }

    //Object.assign():
    // Object.assign(ele.style, custom_style);
    // Object.assign(ele2.style, custom_style2);
    // Object.assign(ele3.style, custom_style3);

}; 