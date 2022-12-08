$(document).ready(function() {
    var dataTable = $('#filtertable6').DataTable({
        "pageLength":10,
        'aoColumnDefs':[{
            'bSortable':false,
            'aTargets':['nosort'],
        }],
        columnDefs:[
            {type:'date-dd-mm-yyyy',aTargets:[5]}
        ],
        "aoColumns":[
            null,
            null,
            null,
            null
        ],
        "order":false,
        "bLengthChange":false,
        "pagingType": "full",
        "dom":'<"top">ct<"top"p><"clear">'
    });
    $("#filterbox6").keyup(function(){
        dataTable.search(this.value).draw();
    });
} );