from isic4kit import ISIC4Classifier

# English examples
isic_en = ISIC4Classifier(language="en")

# Example 1: Get section (Agriculture)
section_en = isic_en.get_section("a")
section_en.print_tree()

# Example 2: Get division (Crop and animal production)
division_en = isic_en.get_division("01")
division_en.print_tree()

# Example 3: Get group (Growing of non-perennial crops)
group_en = isic_en.get_group("011")
group_en.print_tree()

# Example 4: Get class (Growing of cereals)
class_en = isic_en.get_class("0111")
class_en.print_tree()

# Example 5: Search in English
search_en = isic_en.search("mining")
search_en.print_tree()

# Arabic examples
isic_ar = ISIC4Classifier(language="ar")

# Example 1: Get section (الزراعة)
section_ar = isic_ar.get_section("a")
section_ar.print_tree()

# Example 2: Get division (زراعة المحاصيل والإنتاج الحيواني)
division_ar = isic_ar.get_division("01")
division_ar.print_tree()

# Example 3: Get group (زراعة المحاصيل غير الدائمة)
group_ar = isic_ar.get_group("011")
group_ar.print_tree()

# Example 4: Get class (زراعة الحبوب)
class_ar = isic_ar.get_class("0111")
class_ar.print_tree()

# Example 5: Search in Arabic
search_ar = isic_ar.search("تعدين")
search_ar.print_tree()
