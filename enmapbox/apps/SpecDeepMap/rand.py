def unfreeze_first_encoder_layer(self, encoder):
    """
    Unfreeze the first encoder layer for any AMP backbone (conv or transformer).
    This method works generically by finding the first layer in the encoder.
    """
    try:
        # Get the first layer of the encoder
        # For most architectures, this is the first module in the encoder
        first_layer = None
        first_layer_name = None

        # Try to find the first layer by iterating through encoder modules
        for name, module in encoder.named_children():
            first_layer = module
            first_layer_name = name
            break

        if first_layer is not None:
            # Unfreeze all parameters in the first layer
            for param in first_layer.parameters():
                param.requires_grad = True
            print(f"Unfroze first encoder layer '{first_layer_name}': {type(first_layer).__name__}")

            # For debugging: print the structure of the first layer
            if hasattr(first_layer, 'named_children'):
                child_modules = list(first_layer.named_children())
                if child_modules:
                    print(f"  First layer contains {len(child_modules)} sub-modules")
                    for i, (child_name, child_module) in enumerate(child_modules[:3]):  # Show first 3
                        print(f"    {i}: {child_name} -> {type(child_module).__name__}")
                    if len(child_modules) > 3:
                        print(f"    ... and {len(child_modules) - 3} more sub-modules")
        else:
            print("Warning: Could not find first encoder layer to unfreeze")

    except Exception as e:
        print(f"Warning: Could not unfreeze first encoder layer: {e}")
