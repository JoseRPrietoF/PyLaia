output_dir=work_span
mkdir ${output_dir}
dropout=0.5
enc_size=512
model=span_lines
python create_model.py \
--logging.filepath ${output_dir}/train.log \
--logging.level INFO \
--logging.overwrite true \
--common.train_path ${output_dir} \
--model ${model} \
--span.enc_size ${enc_size} \
--span.dropout ${dropout} \
--span.num_input_channels 1 /home/jprieto/data/HisClimaProd/HTR/emilio/symbols.lst

