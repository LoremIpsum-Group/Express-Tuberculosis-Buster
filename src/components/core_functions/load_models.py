from components.core_functions.dependencies_loading import keras, tf, load_model

def load_model_efficientNet(path):
    model = load_model(path)
    return model

def load_model_unet (path):
    # Segment for loading the unet model
    @keras.utils.register_keras_serializable()
    def dice_coef(y_true, y_pred):
        y_true_f = y_true.flatten()
        y_pred_f = y_pred.flatten()
        intersection = keras.sum(y_true_f * y_pred_f)
        return (2.0 * intersection + 1) / (keras.sum(y_true_f) + keras.sum(y_pred_f) + 1)


    @keras.utils.register_keras_serializable()
    def dice_coef_loss(y_true, y_pred):
        return -dice_coef(y_true, y_pred)


    tf.keras.utils.get_custom_objects()["dice_coef_loss"] = dice_coef_loss
    model = load_model(
        path,
        custom_objects={"dice_coef_loss": dice_coef_loss},
    )

    return model
