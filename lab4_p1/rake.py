from multi_rake import Rake
rake = Rake()

full_text = "Tokyo scientists create nanoscrolls for next-gen tech | Researchers achieved a major breakthrough by crafting nanoscrolls using Janus nanosheets. This innovation unlocks doors to exciting possibilities in catalysis, optics, and clean energy."
keywords = rake.apply(full_text)
print(keywords[:10])
