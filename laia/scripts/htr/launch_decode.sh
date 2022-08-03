output_dir=work_small
batch_size=6
img_dirs=/home/jprieto/data/HisClimaProd/HTR/emilio/images/
mkdir ${output_dir}/results
# for partition in "te"; do
for partition in "tr" "val" "te"; do
echo $partition
    python decode_ctc.py \
    --common.train_path ${output_dir} \
    --common.model_filename model \
    --common.checkpoint epoch=0-lowest_va_cer.ckpt \
    --logging.level NOTSET \
    --data.batch_size ${batch_size} \
    --trainer.gpus 1 \
    --trainer.auto_select_gpus true \
    --decode.use_symbols true \
    --logging.to_stderr_level INFO \
    --logging.filepath logs/${partition}_ctc-decoding.log \
    --data.color_mode L \
    --img_dirs [${img_dirs}] \
    /home/jprieto/data/HisClimaProd/HTR/emilio/symbols.lst \
    /home/jprieto/data/HisClimaProd/HTR/emilio/${partition}/list_${partition}.lst > ${output_dir}/results/${partition}_ctc_char.txt

    gawk '{
      printf("%s ", $1);
      for (i=2;i<=NF;++i) {
        if ($i == "<space>")
          printf(" ");
        else
          printf("%s", $i);
      }
      printf("\n");
    }' ${output_dir}/results/${partition}_ctc_char.txt | tr -s ' ' | sed "s|''|\"|g" | sed 's/ $//' > ${output_dir}/results/${partition}_ctc_word.txt
    sed -i 's/.png//g' ${output_dir}/results/${partition}_ctc_word.txt
done