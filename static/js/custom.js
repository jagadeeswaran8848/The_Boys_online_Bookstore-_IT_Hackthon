// static/js/custom.js
function removeItem(productId) {
    // Send an AJAX request to remove the item from the cart
    $.ajax({
      type: 'POST',
      url: '/remove_from_cart',
      data: { product_id: productId },
      success: function(response) {
        // Reload the page or update the cart content as needed
        location.reload();
      },
      error: function(error) {
        console.error('Error removing item from cart:', error);
      }
    });
  }
  