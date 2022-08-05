GradCheck=2
reduceAxis=2
wmul=2.0
nlyrs=4
height=96
use_distortions=true
lszs=[[0,64],[2,128],[4,256]]
# lreszs=[[0,MaxPool2d],[2,MaxPool2d]]
lreszs=[[0,MaxPool2d]]
output_dir=work_small3
model=origaminet
python create_model.py \
--logging.filepath ${output_dir}/train.log \
--logging.level INFO \
--logging.overwrite true \
--common.train_path ${output_dir} \
--model ${model} \
--origaminet.GradCheck ${GradCheck} \
--origaminet.reduceAxis ${reduceAxis} \
--origaminet.wmul ${wmul} \
--origaminet.nlyrs ${nlyrs} \
--origaminet.lszs ${lszs} \
--origaminet.lreszs ${lreszs} \
--origaminet.num_input_channels 1 /home/jprieto/data/HisClimaProd/HTR/emilio/symbols.lst

