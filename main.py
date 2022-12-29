from meal_planner import SkinnyTasteRecipe

my_recipe = SkinnyTasteRecipe("https://www.skinnytaste.com/turkey-stuffed-peppers-45-pts/")
print(my_recipe.get_recipe())

recipe_2 = SkinnyTasteRecipe("https://www.skinnytaste.com/turkey-enchilada-stuffed-poblanos-rellenos/")
print(recipe_2.get_recipe())
