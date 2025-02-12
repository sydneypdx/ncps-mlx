import mlx.core as np
import pytest

from ncps.mini_keras import backend
from ncps.mini_keras import initializers
from ncps.mini_keras import layers
from ncps.mini_keras import testing


class ConvLSTM3DTest(testing.TestCase):
    @pytest.mark.requires_trainable_backend
    def test_basics(self):
        channels_last = backend.config.image_data_format() == "channels_last"
        self.run_layer_test(
            layers.ConvLSTM3D,
            init_kwargs={"filters": 5, "kernel_size": 3, "padding": "same"},
            input_shape=(
                (3, 2, 4, 4, 4, 3) if channels_last else (3, 2, 3, 4, 4, 4)
            ),
            expected_output_shape=(
                (3, 4, 4, 4, 5) if channels_last else (3, 5, 4, 4, 4)
            ),
            expected_num_trainable_weights=3,
            expected_num_non_trainable_weights=0,
            supports_masking=True,
        )
        self.run_layer_test(
            layers.ConvLSTM3D,
            init_kwargs={
                "filters": 5,
                "kernel_size": 3,
                "padding": "valid",
                "recurrent_dropout": 0.5,
            },
            input_shape=(
                (3, 2, 8, 8, 8, 3) if channels_last else (3, 2, 3, 8, 8, 8)
            ),
            call_kwargs={"training": True},
            expected_output_shape=(
                (3, 6, 6, 6, 5) if channels_last else (3, 5, 6, 6, 6)
            ),
            expected_num_trainable_weights=3,
            expected_num_non_trainable_weights=0,
            supports_masking=True,
        )
        self.run_layer_test(
            layers.ConvLSTM3D,
            init_kwargs={
                "filters": 5,
                "kernel_size": 3,
                "padding": "valid",
                "return_sequences": True,
            },
            input_shape=(
                (3, 2, 8, 8, 8, 3) if channels_last else (3, 2, 3, 8, 8, 8)
            ),
            expected_output_shape=(
                (3, 2, 6, 6, 6, 5) if channels_last else (3, 2, 5, 6, 6, 6)
            ),
            expected_num_trainable_weights=3,
            expected_num_non_trainable_weights=0,
            supports_masking=True,
        )

    def test_correctness(self):
        sequence = (
            np.arange(1920).reshape((2, 3, 4, 4, 4, 5)).astype("float32") / 100
        )
        expected_output = np.array(
            [
                [
                    [
                        [[0.99149036, 0.99149036], [0.99180907, 0.99180907]],
                        [[0.99258363, 0.99258363], [0.9927925, 0.9927925]],
                    ],
                    [
                        [[0.99413764, 0.99413764], [0.99420583, 0.99420583]],
                        [[0.9943788, 0.9943788], [0.9944278, 0.9944278]],
                    ],
                ],
                [
                    [
                        [[0.9950547, 0.9950547], [0.9950547, 0.9950547]],
                        [[0.9950547, 0.9950547], [0.9950547, 0.9950547]],
                    ],
                    [
                        [[0.9950547, 0.9950547], [0.9950547, 0.9950547]],
                        [[0.9950547, 0.9950547], [0.9950547, 0.9950547]],
                    ],
                ],
            ]
        )
        if backend.config.image_data_format() == "channels_first":
            sequence = sequence.transpose((0, 1, 5, 2, 3, 4))
            expected_output = expected_output.transpose((0, 4, 1, 2, 3))
        layer = layers.ConvLSTM3D(
            filters=2,
            kernel_size=3,
            kernel_initializer=initializers.Constant(0.01),
            recurrent_initializer=initializers.Constant(0.02),
            bias_initializer=initializers.Constant(0.03),
        )
        output = layer(sequence)
        self.assertAllClose(
            expected_output,
            output,
        )
