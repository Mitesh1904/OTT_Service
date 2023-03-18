function get_img(i = 0) {
    const img = ["https://www.tvseasonspoilers.com/wp-content/uploads/2020/02/Mirzapur-Season-2.jpg", "http://hityaflopmovieworld.com/wp-content/uploads/2020/10/1500x500-715x400.jpg", "https://image.tmdb.org/t/p/w780/9miD6gkNYq2xXZwBfHry9FQjeti.jpg", "https://nettv4u.com/uploads/fast-and-furious-7-review.jpg", "https://th.bing.com/th/id/R9c07f4d73fd758c97b216a6ec00c5301?rik=rC%2b3hp7sWwF%2bhw&riu=http%3a%2f%2fsimplywallpaper.net%2fpictures%2f2011%2f04%2f05%2fblackbeard-Pirates-of-the-Caribbean-wallpaper.jpg&ehk=WBw5HcAPj0vZkCxvAuhssFYtyJbGZ3eHP1pxsrgLj9U%3d&risl=&pid=ImgRaw", "https://th.bing.com/th/id/R6c7c9e1f6957d72754ef42e412a4ab6c?rik=caey91mnnqsfUg&riu=http%3a%2f%2f3.bp.blogspot.com%2f-mHmfp_Uem4M%2fTn7x-fuZOaI%2fAAAAAAAACR0%2fw9aqNgY9mrU%2fs1600%2fPirates-of-the-Caribbean-4-Three-pirates_1680x1050.jpg&ehk=CcMrHXxtzVIGKkHNSpocQskawyVVidsKlyN2Kpd%2beQ8%3d&risl=&pid=ImgRaw", "http://conversationsabouther.net/wp-content/uploads/2017/06/conjuring.jpg", "https://i1.wp.com/urbanasian.com/wp-content/uploads/2018/11/Mirzapur.jpg?fit=1200%2C628&ssl=1"];
    document.getElementById('im1').src = img[i];
    i = i + 1;
    if (i == img.length)
        setTimeout(get_img, 5000, 0);
    else
        setTimeout(get_img, 5000, i);
}

function fun_third() {
    document.getElementById('pay1').style.display = "none";
    console.log("Mitesh")
    document.getElementById('th').style.display = "block"
    document.getElementById('pay2').style.marginTop = "10px";
}
function fun_credit() {
    document.getElementById('pay1').style.display = "none";
    console.log("Mitesh Madrchod")
    document.getElementById('cr').style.display = "block"
    document.getElementById('pay2').style.marginTop = "0px";
}

function subdata() {
    document.getElementById('subscrib').style.display = "none";
    document.getElementById('pay').style.display = "inline";
    document.getElementById('presonal').style.display = "inline";
    document.getElementById('div9').style.display = "none";
    document.getElementById('div11').style.display = "none";
    document.getElementById('div10').style.display = "block";
    document.getElementById('div12').style.display = "none";
}

function presonaldata() {
    document.getElementById('presonal').style.display = "none";
    document.getElementById('subscrib').style.display = "inline";
    document.getElementById('pay').style.display = "inline"
    document.getElementById('div10').style.display = "none";
    document.getElementById('div11').style.display = "none";
    document.getElementById('div9').style.display = "block";
    document.getElementById('div12').style.display = "none";
}

function paydata() {
    document.getElementById('pay').style.display = "none";
    document.getElementById('subscrib').style.display = "inline";
    document.getElementById('presonal').style.display = "inline";
    document.getElementById('div9').style.display = "none";
    document.getElementById('div10').style.display = "none";
    document.getElementById('div11').style.display = "block";
    document.getElementById('div12').style.display = "none";
}

function pass1() {
    document.getElementById('div9').style.display = "none";
    document.getElementById('div10').style.display = "none";
    document.getElementById('div11').style.display = "none";
    document.getElementById('div_btns').style.display = "none";
    document.getElementById('logout_btn').style.display = "none";
    document.getElementById('div12').style.display = "block";
}