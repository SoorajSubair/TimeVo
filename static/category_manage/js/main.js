$(document).ready(function() {
    var dataTable = $('#filtertable4').DataTable({
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
    $("#filterbox4").keyup(function(){
        dataTable.search(this.value).draw();
    });
} );