"use strict";

// take a list of cupcakes and creates
// html elements <ul> and append to the page
// <ul>
/*
<ul>
<img src=`${cupcake.image_url}` >
<li><a href=`/api/cupcakes/${cupcake.id}>
<img src=`${cupcake.image_url}`>
flavor : cupcake.flavor size : cupcake.size`
rating : cupcake.rating </li>

*/

$(".button").on("click", list_cupcakes);

async function list_cupcakes() {
  let cupcakes = await get_cupcakes();
  console.log("cupcakes =", cupcakes);
  let $body = $("body");
  let $ul = $("<ul>");
  $body.append($ul);
  for (let cupcake of cupcakes) {
    let $li = $("<li>").append(`<a href=/api/cupcakes/${cupcake.id}>
     <img height="300px" width="200px" src=${cupcake.image_url}>flavor : ${cupcake.flavor} size : ${cupcake.size}
    rating : ${cupcake.rating}</a>`);
    $ul.append($li);
  }
}

async function get_cupcakes() {
  let cupcakes = await axios.get("http://localhost:5001/api/cupcakes");

  return cupcakes.data.cupcakes;
}
