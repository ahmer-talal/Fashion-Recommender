import pandas as pd
import itertools
import random
def main():
    pass

if __name__ == "__main__":
    main()

# Define attributes
categories = ['T-shirt', 'Kurta', 'Jeans', 'Chinos', 'Blazer', 'Hoodie', 'A-line Dress', 'Maxi Dress', 'Shirt', 'Skirt', 'Sweater', 'Jacket', 'Trouser', 'Blouse', 'Sweatshirt', 'Lehenga', 'Sherwani']
genders = ['Men', 'Women']
colors = ['Black', 'White', 'Navy', 'Maroon', 'Beige', 'Green', 'Grey', 'Brown', 'Olive', 'Blue', 'Red', 'Cream', 'Teal', 'Mustard', 'Coral', 'Lavender', 'Charcoal', 'Turquoise', 'Pink', 'Burgundy', 'Mint', 'Peach', 'Gold', 'Silver', 'Indigo', 'Violet', 'Khaki', 'Rust', 'Sky Blue', 'Emerald']
styles = ['Casual', 'Business Casual', 'Formal', 'Traditional', 'Party']
price_ranges = ['Low', 'Medium', 'High', 'Premium']
body_types = ['Rectangle', 'Hourglass', 'Pear', 'Apple', 'Inverted Triangle']
skin_tones = ['Fair', 'Medium', 'Tan', 'Olive', 'Dark']
face_shapes = ['Oval', 'Round', 'Square', 'Diamond', 'Heart']
height_ranges = ['Short', 'Average', 'Tall']
fits = ['Slim-fit', 'Loose', 'Flared', 'Straight-cut', 'A-line', 'Fitted']
necklines = ['Crew neck', 'V-neck', 'Scoop neck', 'Collared', 'Mandarin collar', 'Round neck']
sleeve_lengths = ['Sleeveless', 'Short-sleeve', '3/4 sleeve', 'Long-sleeve']
hemlines = ['Cropped', 'Midi', 'Mini', 'Maxi', 'Ankle-length']
waistlines = ['Low-rise', 'Mid-rise', 'High-waist']
occasions = ['Casual', 'Formal', 'Ethnic', 'Evening Wear', 'Business']
fabrics = ['Cotton', 'Linen', 'Silk', 'Denim', 'Wool', 'Chiffon', 'Velvet', 'Georgette', 'Satin']
seasons = ['Summer', 'Winter', 'All-season']

# Constraints
category_constraints = {
    'T-shirt': {'genders': ['Men', 'Women'], 'styles': ['Casual'], 'occasions': ['Casual'], 'fits': ['Slim-fit', 'Loose'], 'necklines': ['Crew neck', 'V-neck'], 'sleeve_lengths': ['Short-sleeve'], 'hemlines': ['Cropped'], 'seasons': ['Summer', 'All-season']},
    'Kurta': {'genders': ['Men', 'Women'], 'styles': ['Traditional'], 'occasions': ['Ethnic'], 'fits': ['A-line', 'Straight-cut'], 'necklines': ['Mandarin collar'], 'sleeve_lengths': ['3/4 sleeve', 'Long-sleeve'], 'hemlines': ['Midi', 'Maxi'], 'seasons': ['Summer', 'All-season']},
    'Jeans': {'genders': ['Men', 'Women'], 'styles': ['Casual'], 'occasions': ['Casual'], 'fits': ['Slim-fit', 'Flared'], 'hemlines': ['Cropped', 'Ankle-length'], 'waistlines': ['Mid-rise', 'High-waist'], 'seasons': ['All-season']},
    'Chinos': {'genders': ['Men'], 'styles': ['Business Casual'], 'occasions': ['Business'], 'fits': ['Slim-fit'], 'hemlines': ['Ankle-length'], 'waistlines': ['Mid-rise'], 'seasons': ['All-season']},
    'Blazer': {'genders': ['Men'], 'styles': ['Formal'], 'occasions': ['Formal', 'Business'], 'fits': ['Slim-fit'], 'necklines': ['Collared'], 'sleeve_lengths': ['Long-sleeve'], 'hemlines': ['Midi'], 'seasons': ['Winter', 'All-season']},
    'Hoodie': {'genders': ['Men', 'Women'], 'styles': ['Casual'], 'occasions': ['Casual'], 'fits': ['Loose'], 'necklines': ['Crew neck'], 'sleeve_lengths': ['Long-sleeve'], 'hemlines': ['Cropped'], 'seasons': ['Winter']},
    'A-line Dress': {'genders': ['Women'], 'styles': ['Casual', 'Party'], 'occasions': ['Casual', 'Evening Wear'], 'fits': ['A-line'], 'necklines': ['V-neck', 'Scoop neck'], 'sleeve_lengths': ['Sleeveless', 'Short-sleeve'], 'hemlines': ['Midi', 'Maxi'], 'seasons': ['Summer']},
    'Maxi Dress': {'genders': ['Women'], 'styles': ['Party'], 'occasions': ['Evening Wear'], 'fits': ['A-line'], 'necklines': ['V-neck'], 'sleeve_lengths': ['Sleeveless'], 'hemlines': ['Maxi'], 'seasons': ['Summer']},
    'Shirt': {'genders': ['Men', 'Women'], 'styles': ['Business Casual', 'Formal'], 'occasions': ['Business', 'Formal'], 'fits': ['Slim-fit', 'Fitted'], 'necklines': ['Collared'], 'sleeve_lengths': ['Short-sleeve', 'Long-sleeve'], 'hemlines': ['Cropped'], 'seasons': ['All-season']},
    'Skirt': {'genders': ['Women'], 'styles': ['Casual'], 'occasions': ['Casual'], 'fits': ['A-line', 'Flared'], 'hemlines': ['Mini', 'Midi'], 'waistlines': ['High-waist'], 'seasons': ['Summer']},
    'Sweater': {'genders': ['Men', 'Women'], 'styles': ['Casual'], 'occasions': ['Casual'], 'fits': ['Loose'], 'necklines': ['Crew neck', 'V-neck'], 'sleeve_lengths': ['Long-sleeve'], 'hemlines': ['Midi'], 'seasons': ['Winter']},
    'Jacket': {'genders': ['Men'], 'styles': ['Casual', 'Formal'], 'occasions': ['Casual', 'Formal'], 'fits': ['Slim-fit'], 'necklines': ['Collared'], 'sleeve_lengths': ['Long-sleeve'], 'hemlines': ['Cropped'], 'seasons': ['Winter']},
    'Trouser': {'genders': ['Men', 'Women'], 'styles': ['Business Casual'], 'occasions': ['Business'], 'fits': ['Slim-fit', 'Straight-cut'], 'hemlines': ['Ankle-length'], 'waistlines': ['Mid-rise'], 'seasons': ['All-season']},
    'Blouse': {'genders': ['Women'], 'styles': ['Casual', 'Formal'], 'occasions': ['Casual', 'Business'], 'fits': ['Slim-fit', 'Loose'], 'necklines': ['V-neck', 'Collared'], 'sleeve_lengths': ['Short-sleeve', '3/4 sleeve'], 'hemlines': ['Cropped'], 'seasons': ['Summer', 'All-season']},
    'Sweatshirt': {'genders': ['Men', 'Women'], 'styles': ['Casual'], 'occasions': ['Casual'], 'fits': ['Loose'], 'necklines': ['Crew neck'], 'sleeve_lengths': ['Long-sleeve'], 'hemlines': ['Cropped'], 'seasons': ['Winter']},
    'Lehenga': {'genders': ['Women'], 'styles': ['Traditional', 'Party'], 'occasions': ['Ethnic', 'Evening Wear'], 'fits': ['A-line'], 'hemlines': ['Maxi'], 'seasons': ['All-season']},
    'Sherwani': {'genders': ['Men'], 'styles': ['Traditional', 'Formal'], 'occasions': ['Ethnic', 'Formal'], 'fits': ['Fitted'], 'necklines': ['Mandarin collar'], 'sleeve_lengths': ['Long-sleeve'], 'hemlines': ['Maxi'], 'seasons': ['All-season']}
}
color_suitability = {
    'Apple': ['Black', 'Navy', 'Charcoal', 'Burgundy', 'Indigo', 'Olive', 'Maroon'],
    'Pear': ['Black', 'Maroon', 'Olive', 'Indigo', 'Grey', 'Brown'],
    'Rectangle': ['Coral', 'Mint', 'Sky Blue', 'Lavender', 'Peach', 'Pink', 'Mustard'],
    'Hourglass': ['Red', 'Teal', 'Emerald', 'Pink', 'Violet', 'Gold'],
    'Inverted Triangle': ['Navy', 'Green', 'Mustard', 'Rust', 'Khaki'],
    'Fair': ['Red', 'Blue', 'Pink', 'Mint', 'Lavender', 'Sky Blue'],
    'Medium': ['Teal', 'Coral', 'Mustard', 'Olive', 'Peach'],
    'Tan': ['Cream', 'Gold', 'Emerald', 'Rust', 'Khaki'],
    'Olive': ['Burgundy', 'Indigo', 'Silver', 'Violet', 'Brown'],
    'Dark': ['Mustard', 'Olive', 'Cream', 'Gold', 'White', 'Beige']
}

# Generate combinations
combinations = []
for category in categories:
    valid_genders = category_constraints[category]['genders']
    valid_styles = category_constraints[category]['styles']
    valid_seasons = category_constraints[category]['seasons']
    valid_colors = colors
    for gender, style, season, color in itertools.product(valid_genders, valid_styles, valid_seasons, valid_colors):
        combinations.append((category, gender, style, season, color))
random.shuffle(combinations)
max_rows = 2000
combinations = combinations[:max_rows]

# Helper function for random subset
def random_subset(lst, min_items=1, max_items=2):
    return '|'.join(random.sample(lst, random.randint(min_items, min(max_items, len(lst)))))

# Create dataset
data = []
for idx, (category, gender, style, season, color) in enumerate(combinations):
    item_id = f"ITM{idx+1:05d}"
    name = f"{color} {category}"
    constraints = category_constraints[category]
    
    # Color suitability check
    suitable_body_types = random_subset(body_types)
    suitable_skin_tones = random_subset(skin_tones)
    body_type_list = suitable_body_types.split('|')
    skin_tone_list = suitable_skin_tones.split('|')
    if not (any(color in color_suitability.get(bt, colors) for bt in body_type_list) or any(color in color_suitability.get(st, colors) for st in skin_tone_list)):
        continue
    
    row_data = {
        'item_id': item_id,
        'category': category,
        'gender': gender,
        'name': name,
        'color': color,
        'style': style,
        'price_range': random.choice(price_ranges),
        'suitable_body_type': suitable_body_types,
        'suitable_skin_tone': suitable_skin_tones,
        'suitable_face_shape': random_subset(face_shapes),
        'suitable_height_range': random_subset(height_ranges),
        'fit': random.choice(constraints.get('fits', fits)),
        'neckline': random.choice(constraints.get('necklines', [''])) if constraints.get('necklines') else '',
        'sleeve_length': random.choice(constraints.get('sleeve_lengths', [''])) if constraints.get('sleeve_lengths') else '',
        'hemline': random.choice(constraints.get('hemlines', hemlines)),
        'waistline': random.choice(constraints.get('waistlines', [''])) if constraints.get('waistlines') else '',
        'occasion': random.choice(constraints.get('occasions', occasions)),
        'fabric': random.choice(fabrics),
        'season': season
    }
    data.append(row_data)

# Create DataFrame
df = pd.DataFrame(data)

# Save as TSV
df.to_csv('improved_fashion_dataset_detailed.txt', sep='\t', index=False, encoding='utf-8')

print("Generated: improved_fashion_dataset_detailed.txt")
