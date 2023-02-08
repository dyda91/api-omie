function edit_row(no) {
    document.getElementById("edit_button" + no).style.display = "none";
    document.getElementById("save_button" + no).style.display = "block";
   
    let codigo = document.getElementById("novo_item" + no);
    let descricao = document.getElementById("nova_descricao" + no);
    let quantidade = document.getElementById("nova_quantidade" + no);
   
    let codigo_data = codigo.innerHTML;
    let descricao_data = descricao.innerHTML;
    let quantidade_data = quantidade.innerHTML;
   
    codigo.innerHTML =
     "<input type='text' id='codigo_text" + no + "' value='" + codigo_data + "'>";
    descricao.innerHTML =
     "<input type='text' id='descricao_text" +
     no +codigo
     "' value='" +
     descricao_data +
     "'>";
    quantidade.innerHTML =
     "<input type='text' id='quantidade_text" + no + "' value='" + quantidade_data + "'>";
   }
   
   function save_row(no) {
    let codigo_val = document.getElementById("codigo_text" + no).value;
    let descricao_val = document.getElementById("descricao_text" + no).value;
    let quantidade_val = document.getElementById("quantidade_text" + no).value;
   
    document.getElementById("novo_item" + no).innerHTML = codigo_val;
    document.getElementById("nova_descricao" + no).innerHTML = descricao_val;
    document.getElementById("nova_quantidade" + no).innerHTML = quantidade_val;
   
    document.getElementById("edit_button" + no).style.display = "block";
    document.getElementById("save_button" + no).style.display = "none";
   }
   
   function delete_row(no) {
    document.getElementById("row" + no + "").outerHTML = "";
   }
   
   function add_row() {
    let codigo_item = document.getElementById("codigo_item").value;
    let descricao_item = document.getElementById("descricao_item").value;
    let quantidade_item = document.getElementById("quantidade_item").value;
   
    let table = document.getElementById("data_table");
    let table_len = table.rows.length - 1;
    let row = (table.insertRow(table_len).outerHTML =
     "<tr id='row" +
     table_len +
     "'><td id='novo_item" +
     table_len +
     "'>" +
     codigo_item +
     "</td><td id='nova_descricao" +
     table_len +
     "'>" +
     descricao_item +
     "</td><td id='nova_quantidade" +
     table_len +
     "'>" +
     quantidade_item +
     "</td><td><input type='button' id='edit_button" +
     table_len +
     "' value='Edit' class='edit' onclick='edit_row(" +
     table_len +
     ")'> <input type='button' id='save_button" +
     table_len +
     "' value='Save' class='save' onclick='save_row(" +
     table_len +
     ")'> <input type='button' value='Delete' class='delete' onclick='delete_row(" + table_len + ")'></td></tr>");
   
    document.getElementById("codigo_item").value = "";
    document.getElementById("descricao_item").value = "";
    document.getElementById("quantidade_item").value = "";
   }
   