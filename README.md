# Albert Heijn (unofficial) REST interface

New features are being added

# Installation
    pip install albert

# Usage

### Initalize API
    import albert
    ah = albert.Api("username","password")
Make an account on ah.nl.
### Add product to cart    
    ah.add("wi386562",amount=30)
You can find products on www.albertheijn.nl. I.e., https://www.ah.nl/producten2/product/wi383655/ah-conference-peren
By default, one item is added to cart if you dont pass the second parameter.

###  Items in cart
    ah.cart()

### Empty cart
    ah.empty()

### Save cart to list
    ah.shopping_list_add("Name of List", empty_card=False)
Standard after calling shopping_list_add method, by Default, the items in your cart will remain. When passing the second argument as True, the items will get removed from your cart after saving the cart items to list.

### Product Information
    ah_product = albert.Product('wi60539/ah-scharrelei-advocaat')
    print(ah_product.id)

pass the query without producten/product/ from a product as string argument to retrieve information from the product. Several items can be accessed:
- `id`
- `name`
- `brand`
- `description`
- `summary`
- `unit_size`
- `category`
- `is_available`
- `priceLabel`
- `price_current`
- `price_previous`
- `is_discounted`
