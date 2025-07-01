function addToCart(name, price) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, price: price })
    }).then(res => res.json())
      .then(data => alert("Added to cart!"));
}
