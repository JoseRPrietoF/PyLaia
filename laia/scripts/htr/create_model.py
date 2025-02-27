#!/usr/bin/env python3
from typing import Any, Dict, List, Optional

import jsonargparse
import torch.nn as nn
from jsonargparse.typing import NonNegativeInt
from pytorch_lightning import seed_everything

import laia.common.logging as log
from laia.common.arguments import CommonArgs, CreateCRNNArgs, CreateOrigamiNetArgs, CreateSPANArgs
from laia.common.saver import ModelSaver
from laia.models.htr import LaiaCRNN
from laia.models.htr.SPAN import SPAN_lines
from laia.models.htr.cnv_model import OrigamiNet
from laia.scripts.htr import common_main
from laia.utils import SymbolsTable

def run(
    syms: str,
    fixed_input_height: Optional[NonNegativeInt] = 0,
    adaptive_pooling: str = "avgpool-16",
    common: CommonArgs = CommonArgs(),
    crnn: CreateCRNNArgs = CreateCRNNArgs(),
    origaminet: CreateOrigamiNetArgs = CreateOrigamiNetArgs(),
    span: CreateSPANArgs = CreateSPANArgs(),
    save_model: bool = False,
    model: str = "pylaia"
) -> LaiaCRNN:
    seed_everything(common.seed)

    crnn.num_output_labels = len(SymbolsTable(syms))
    origaminet.num_output_labels = len(SymbolsTable(syms))
    span.num_output_labels = len(SymbolsTable(syms))
    if crnn is not None:
        if fixed_input_height:
            conv_output_size = LaiaCRNN.get_conv_output_size(
                size=(fixed_input_height, fixed_input_height),
                cnn_kernel_size=crnn.cnn_kernel_size,
                cnn_stride=crnn.cnn_stride,
                cnn_dilation=crnn.cnn_dilation,
                cnn_poolsize=crnn.cnn_poolsize,
            )
            fixed_size_after_conv = conv_output_size[1 if crnn.vertical_text else 0]
            assert (
                fixed_size_after_conv > 0
            ), "The image size is too small for the CNN architecture"
            crnn.image_sequencer = f"none-{fixed_size_after_conv}"
        else:
            crnn.image_sequencer = adaptive_pooling
        crnn.rnn_type = getattr(nn, crnn.rnn_type)
        crnn.cnn_activation = [getattr(nn, act) for act in crnn.cnn_activation]

    if model == "pylaia":
        model_net = LaiaCRNN(**vars(crnn))
    elif model == "origaminet":
        model_net = OrigamiNet(**vars(origaminet))
        print(model_net)
    elif model == "span_lines":
        model_net = SPAN_lines(**vars(span))
        print(model_net)
    else:
        raise Exception(f"Model {common.model} not supported.")
    log.info(
        "Model has {} parameters",
        sum(param.numel() for param in model_net.parameters()),
    )
    if save_model:
        if model == "pylaia":
            ModelSaver(common.train_path, common.model_filename).save(
                LaiaCRNN, **vars(crnn)
            )
        elif model == "origaminet":
            
            ModelSaver(common.train_path, common.model_filename).save(
                OrigamiNet, **vars(origaminet)
            )
    return model_net


def get_args(argv: Optional[List[str]] = None) -> Dict[str, Any]:
    parser = jsonargparse.ArgumentParser(
        parse_as_dict=True,
        description=(
            "Create a model for HTR composed of a set of convolutional blocks, followed"
            " by a set of bidirectional RNN layers, and a final linear layer. Each"
            " convolutional block is composed by a 2D convolutional layer, an optional"
            " batch normalization layer, a non-linear activation function, and an"
            " optional 2D max-pooling layer. A dropout layer might precede each"
            " block, rnn layer, and the final linear layer"
        ),
    )
    parser.add_argument(
        "--config", action=jsonargparse.ActionConfigFile, help="Configuration file"
    )
    parser.add_argument(
        "syms",
        type=str,
        help=(
            "Mapping from strings to integers. "
            "The CTC symbol must be mapped to integer 0"
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default="pylaia",
        help=(
            "Type of model. pylaia by default. "
            "Models supported: pylaia origaminet span_lines"
        ),
    )
    parser.add_argument(
        "--fixed_input_height",
        type=NonNegativeInt,
        default=0,
        help=(
            "Height of the input images. If 0, a variable height model "
            "will be used (see `adaptive_pooling`). This will be used to compute the "
            "model output height at the end of the convolutional layers"
        ),
    )
    parser.add_argument(
        "--adaptive_pooling",
        type=str,
        default="avgpool-16",
        help=(
            "Use our custom adaptive pooling layers. This option allows training with"
            " variable height images. Takes into account the size of each individual"
            " image within the bach (before padding). (allowed: {avg,max}pool-N)"
        ),
    )
    parser.add_argument(
        "--save_model",
        type=bool,
        default=True,
        help="Whether to save the model to a file",
    )

    parser.add_class_arguments(CommonArgs, "common")
    parser.add_function_arguments(log.config, "logging")
    parser.add_class_arguments(CreateCRNNArgs, "crnn")
    parser.add_class_arguments(CreateOrigamiNetArgs, "origaminet")
    parser.add_class_arguments(CreateSPANArgs, "span")

    args = parser.parse_args(argv, with_meta=False)

    args["common"] = CommonArgs(**args["common"])
    args["crnn"] = CreateCRNNArgs(**args["crnn"])
    args["origaminet"] = CreateOrigamiNetArgs(**args["origaminet"])
    args["span"] = CreateSPANArgs(**args["span"])

    return args


def main():
    args = get_args()
    args = common_main(args)
    run(**args)


if __name__ == "__main__":
    main()
