// let itensData = '{{ json }}'

// // buildTable(itensData)


// for (var i in itensData){
//     var row = `<tr>
//                      <td>${itensData[i].pagina}</td>
//                 </tr>`

//     var table = $('#myTable')
//     table.append(row)

// }

// $.ajax({
//     method:'POST',
//     url:'https://app.omie.com.br/api/v1/geral/produtos/',   
//     contentType: "application/json; charset=utf-8",
//     dataType: 'jsonp',
//     data: {
//         "call":"ListarProdutos",
//         "app_key":"706444293555",
//         "app_secret":"a51654af368ec4e34129dab2b017dab7",
//         "param":[{
//                 "pagina":1,
//                 "registros_por_pagina":7000,
//                 "apenas_importado_api":"N",
//                 "filtrar_apenas_omiepdv":"N"		
//             }
//         ]},
//     success:function(response){
// 		itensData = response.data
// 		buildTable(itensData)
// 		console.log(itensData)
//         console.log(response.data)
// 	}
// })


// function buildTable(data){
//     var table = document.getElementById('myTable')

//     for (var i = 0; i < data.length; i++){
//         var row = `<tr>
//                         <td>${data[i].pagina}</td>
//                         <td>${data[i].pagina}</td>
//                         <td>${data[i].pagina}</td>
//                   </tr>`
//         table.innerHTML += row

//     }
// }