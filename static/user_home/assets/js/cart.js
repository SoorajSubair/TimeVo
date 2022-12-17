var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var quantity = this.dataset.id
        var total = this.dataset.total
        var remove = this.dataset.remove

        if(user == 'AnonymousUser'){
            addCookieItem(productId, action,quantity, total, remove)

        }else{
            updateUserOrder(productId, action, quantity, total, remove)
        }
    })
}


function addCookieItem(productId, action,quantity, total, remove){

    if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

    if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}

	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	// location.reload()
    $.ajax({
        type: "GET",
        data: {
            'id':productId
        },

        url : "update_item_guest",
        success: function(response){
            try {
                document.getElementById(quantity).innerHTML = response.item_quantity
                document.getElementById(total).innerHTML = response.item_total
                if(response.item_quantity <= 1){
                    $(remove).addClass('d-none');
                }else{
                    $(remove).removeClass('d-none');
                }
                }
              catch(err) {
                $(".alerts").delay("fast").slideDown().slideUp(1500);
              }
            $(".item-count").html(response.cartItems);
            $("#cart-items").html(response.cartItems);
            $("#bag-total").html(response.bag_total);
            $("#order-total").html(response.total);
        }
    });
}

function updateUserOrder(productId, action, quantity, total, remove){
    var id = id
    $.ajax({
        type: "GET",
        data: {
            'productId':productId,
            'action':action,
        },

        url : "update_item",
        success: function(response){
            try {
                document.getElementById(quantity).innerHTML = response.item_quantity
                document.getElementById(total).innerHTML = response.item_total
                if(response.item_quantity <= 1){
                    $(remove).addClass('d-none');
                }else{
                    $(remove).removeClass('d-none');
                }
                }
              catch(err) {
                $(".alerts").delay("fast").slideDown().slideUp(1500);
              }
            $(".item-count").html(response.cartItems);
            $("#cart-items").html(response.cartItems);
            $("#bag-total").html(response.bag_total);
            $("#order-total").html(response.total);
            
        },
        
    });
}
