$(document).ready(function() {
    var dataTable = $('#filtertable3').DataTable({
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
            null,
            null,
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
    $("#filterbox3").keyup(function(){
        dataTable.search(this.value).draw();
    });
} );