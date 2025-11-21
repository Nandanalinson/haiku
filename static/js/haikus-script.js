
window.addEventListener('load', function() {


    fetch('/api/haikus',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {

        console.log("Data: " + data.haiku)
        //d = data.haiku.replace(/\n/g, ':')
        //document.getElementById('haikus-list').innerHTML = document.body.innerHTML.replaceAll(/,/g, ":")
        // document.getElementById('haikus-list').innerHTML=`<p style="white-space: pre-line; text-transform: capitalize; margin: 5px; " >${data.haiku}</p>`
        //let formattedHaiku = data.haiku.replaceAll(",", ":");
        //let haikuarray = data.haiku.map( => item.replace(/,/g, ""));
        document.getElementById('haikus-list').innerHTML = `<p style="white-space: pre-line; text-transform: capitalize; margin: 5px;">
        ${data.haiku}</p>`

    })
})