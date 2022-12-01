const imagebox1 = document.getElementById("image-box1");
const crop_btn1 = document.getElementById("crop-btn1");
const input1 = document.getElementById("image");

// When user uploads the image this event will get triggered


input1.addEventListener("change", () => {
    // Getting image file object from the input variable
    const img_data1 = input1.files[0];

    // createObjectURL() static method creates a DOMString containing a URL representing the object given in the parameter.
    // The new object URL represents the specified File object or Blob object.
    const url1 = URL.createObjectURL(img_data1);
    // Creating a image tag inside imagebox which will hold the cropping view image(uploaded file) to it using the url created before.
    imagebox1.innerHTML = `<img src="${url1}" id="image1" style="width:100%;">`;
    // Storing that cropping view image in a variable
    const image1 = document.getElementById("image1");
    // Displaying the image box
    document.getElementById("image-box1").style.display = "block";
    // Displaying the Crop buttton
    document.getElementById("crop-btn1").style.display = "block";
    // Hiding the Post button
    document.getElementById("image").style.display = "block";
    const cropper1 = new Cropper(image1, {
        autoCropArea: 1,
        viewMode: 1,
        scalable: true,
        zoomable: true,
        movable: true,
        minCropBoxWidth: 50,
        minCropBoxHeight: 50,
    });
    // When crop button is clicked this event will get triggered
    crop_btn1.addEventListener("click", () => {
        // This method coverts the selected cropped image on the cropper canvas into a blob object
        cropper1.getCroppedCanvas().toBlob((blob) => {
            // Gets the original image data
            let fileInputElement1 = document.getElementById("image");
            // Make a new cropped image file using that blob object, image_data.name will make the new file name same as original image
            let file1 = new File([blob], img_data1.name, {
                type: "image/*",
                lastModified: new Date().getTime(),
            });
            // Create a new container
            let container1 = new DataTransfer();
            // Add the cropped image file to the container
            container1.items.add(file1);
            // Replace the original image file with the new cropped image file
            fileInputElement1.files = container1.files;
            document.getElementById("image").src = URL.createObjectURL(
                fileInputElement1.files[0]

            );
            // Hide the cropper box
            document.getElementById("image-box1").style.display = "none";
            // Hide the crop button
            document.getElementById("crop-btn1").style.display = "none";

        });
    });
});









