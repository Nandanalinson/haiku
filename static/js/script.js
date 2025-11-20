document.getElementById('haiku-form').addEventListener('submit' , function(event){
    event.preventDefault();


    const themeInput = document.getElementById('theme');
    const theme = themeInput ? themeInput.value.trim() : '';

    console.log("Theme:", theme);

    fetch('/generate-haiku',{
        method : 'POST',
        headers : {
            'content-type' : 'application/json'
        },
        body : JSON.stringify({ theme : theme})
    })
    .then(response => response.json())
    .then(data => { 
        document.getElementById('haiku-result').innerHTML = `<p>${data.haiku}</p>`;

    })
    .catch(error => {
        console.error('Error:', error);
    });


    });