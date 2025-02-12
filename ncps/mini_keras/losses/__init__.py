import inspect

from ncps.mini_keras.api_export import keras_mini_export
from ncps.mini_keras.losses.loss import Loss
from ncps.mini_keras.losses.losses import CTC
from ncps.mini_keras.losses.losses import BinaryCrossentropy
from ncps.mini_keras.losses.losses import BinaryFocalCrossentropy
from ncps.mini_keras.losses.losses import CategoricalCrossentropy
from ncps.mini_keras.losses.losses import CategoricalFocalCrossentropy
from ncps.mini_keras.losses.losses import CategoricalHinge
from ncps.mini_keras.losses.losses import Circle
from ncps.mini_keras.losses.losses import CosineSimilarity
from ncps.mini_keras.losses.losses import Dice
from ncps.mini_keras.losses.losses import Hinge
from ncps.mini_keras.losses.losses import Huber
from ncps.mini_keras.losses.losses import KLDivergence
from ncps.mini_keras.losses.losses import LogCosh
from ncps.mini_keras.losses.losses import LossFunctionWrapper
from ncps.mini_keras.losses.losses import MeanAbsoluteError
from ncps.mini_keras.losses.losses import MeanAbsolutePercentageError
from ncps.mini_keras.losses.losses import MeanSquaredError
from ncps.mini_keras.losses.losses import MeanSquaredLogarithmicError
from ncps.mini_keras.losses.losses import Poisson
from ncps.mini_keras.losses.losses import SparseCategoricalCrossentropy
from ncps.mini_keras.losses.losses import SquaredHinge
from ncps.mini_keras.losses.losses import Tversky
from ncps.mini_keras.losses.losses import binary_crossentropy
from ncps.mini_keras.losses.losses import binary_focal_crossentropy
from ncps.mini_keras.losses.losses import categorical_crossentropy
from ncps.mini_keras.losses.losses import categorical_focal_crossentropy
from ncps.mini_keras.losses.losses import categorical_hinge
from ncps.mini_keras.losses.losses import circle
from ncps.mini_keras.losses.losses import cosine_similarity
from ncps.mini_keras.losses.losses import ctc
from ncps.mini_keras.losses.losses import dice
from ncps.mini_keras.losses.losses import hinge
from ncps.mini_keras.losses.losses import huber
from ncps.mini_keras.losses.losses import kl_divergence
from ncps.mini_keras.losses.losses import log_cosh
from ncps.mini_keras.losses.losses import mean_absolute_error
from ncps.mini_keras.losses.losses import mean_absolute_percentage_error
from ncps.mini_keras.losses.losses import mean_squared_error
from ncps.mini_keras.losses.losses import mean_squared_logarithmic_error
from ncps.mini_keras.losses.losses import poisson
from ncps.mini_keras.losses.losses import sparse_categorical_crossentropy
from ncps.mini_keras.losses.losses import squared_hinge
from ncps.mini_keras.losses.losses import tversky
from ncps.mini_keras.saving import serialization_lib

ALL_OBJECTS = {
    # Base
    Loss,
    LossFunctionWrapper,
    # Probabilistic
    KLDivergence,
    Poisson,
    BinaryCrossentropy,
    BinaryFocalCrossentropy,
    CategoricalCrossentropy,
    CategoricalFocalCrossentropy,
    SparseCategoricalCrossentropy,
    # Regression
    MeanSquaredError,
    MeanAbsoluteError,
    MeanAbsolutePercentageError,
    MeanSquaredLogarithmicError,
    CosineSimilarity,
    LogCosh,
    Huber,
    # Hinge
    Hinge,
    SquaredHinge,
    CategoricalHinge,
    # Image segmentation
    Dice,
    Tversky,
    # Similarity
    Circle,
    # Sequence
    CTC,
    # Probabilistic
    kl_divergence,
    poisson,
    binary_crossentropy,
    binary_focal_crossentropy,
    categorical_crossentropy,
    categorical_focal_crossentropy,
    sparse_categorical_crossentropy,
    # Regression
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_logarithmic_error,
    cosine_similarity,
    log_cosh,
    huber,
    # Hinge
    hinge,
    squared_hinge,
    categorical_hinge,
    # Image segmentation
    dice,
    tversky,
    # Similarity
    circle,
    # Sequence
    ctc,
}

ALL_OBJECTS_DICT = {cls.__name__: cls for cls in ALL_OBJECTS}
ALL_OBJECTS_DICT.update(
    {
        "bce": binary_crossentropy,
        "BCE": binary_crossentropy,
        "kld": kl_divergence,
        "KLD": kl_divergence,
        "mae": mean_absolute_error,
        "MAE": mean_absolute_error,
        "mse": mean_squared_error,
        "MSE": mean_squared_error,
        "mape": mean_absolute_percentage_error,
        "MAPE": mean_absolute_percentage_error,
        "msle": mean_squared_logarithmic_error,
        "MSLE": mean_squared_logarithmic_error,
    }
)


@keras_mini_export("ncps.mini_keras.losses.serialize")
def serialize(loss):
    """Serializes loss function or `Loss` instance.

    Args:
        loss: A Keras `Loss` instance or a loss function.

    Returns:
        Loss configuration dictionary.
    """
    return serialization_lib.serialize_keras_object(loss)


@keras_mini_export("ncps.mini_keras.losses.deserialize")
def deserialize(name, custom_objects=None):
    """Deserializes a serialized loss class/function instance.

    Args:
        name: Loss configuration.
        custom_objects: Optional dictionary mapping names (strings) to custom
            objects (classes and functions) to be considered during
            deserialization.

    Returns:
        A Keras `Loss` instance or a loss function.
    """
    return serialization_lib.deserialize_keras_object(
        name,
        module_objects=ALL_OBJECTS_DICT,
        custom_objects=custom_objects,
    )


@keras_mini_export("ncps.mini_keras.losses.get")
def get(identifier):
    """Retrieves a Keras loss as a `function`/`Loss` class instance.

    The `identifier` may be the string name of a loss function or `Loss` class.

    >>> loss = losses.get("categorical_crossentropy")
    >>> type(loss)
    <class 'function'>
    >>> loss = losses.get("CategoricalCrossentropy")
    >>> type(loss)
    <class '...CategoricalCrossentropy'>

    You can also specify `config` of the loss to this function by passing dict
    containing `class_name` and `config` as an identifier. Also note that the
    `class_name` must map to a `Loss` class

    >>> identifier = {"class_name": "CategoricalCrossentropy",
    ...               "config": {"from_logits": True}}
    >>> loss = losses.get(identifier)
    >>> type(loss)
    <class '...CategoricalCrossentropy'>

    Args:
        identifier: A loss identifier. One of None or string name of a loss
            function/class or loss configuration dictionary or a loss function
            or a loss class instance.

    Returns:
        A Keras loss as a `function`/ `Loss` class instance.
    """
    if identifier is None:
        return None
    if isinstance(identifier, dict):
        obj = deserialize(identifier)
    elif isinstance(identifier, str):
        obj = ALL_OBJECTS_DICT.get(identifier, None)
    else:
        obj = identifier

    if callable(obj):
        if inspect.isclass(obj):
            obj = obj()
        return obj
    else:
        raise ValueError(f"Could not interpret loss identifier: {identifier}")
