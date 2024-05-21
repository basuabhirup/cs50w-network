let newPostForm;
let newPost;

document.addEventListener("DOMContentLoaded", () => {
  newPostForm = document.querySelector("#new-post-form");
  newPostContent = document.querySelector("#new-post");
});

const onNewPost = (e) => {
  e.preventDefault();
  console.log(newPostContent.value);
  // API Call
  fetch("/posts", {
    method: "POST",
    body: JSON.stringify({
      content: newPostContent.value,
    }),
  }).then((res) => {
    if (res.status === 201) {
      newPostContent.value = "";
    }
  });
};
