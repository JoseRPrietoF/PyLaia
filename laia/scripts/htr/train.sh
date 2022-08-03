output_dir=work_small
batch_size=3;
learning_rate=0.002;
max_epochs=500;
use_distortions=true;
early_stopping=60
img_dirs=/home/jprieto/data/HisClimaProd/HTR/emilio/images
trans_tr=/home/jprieto/data/HisClimaProd/HTR/emilio/tr/transcriptions_train_char.txt    
trans_val=/home/jprieto/data/HisClimaProd/HTR/emilio/val/transcriptions_val_char.txt
python train_ctc.py \
--logging.filepath  ${output_dir}/train.log \
--train.early_stopping_patience ${early_stopping} \
--logging.level INFO \
--logging.overwrite false \
--common.train_path ${output_dir} \
--optimizer.learning_rate ${learning_rate} \
--train.delimiters ["<space>"] \
--trainer.max_epochs ${max_epochs} \
--data.batch_size ${batch_size} \
--data.color_mode L \
--train.augment_training true \
--trainer.gpus 1 \
--trainer.auto_select_gpus true \
--train.gpu_stat true \
/home/jprieto/data/HisClimaProd/HTR/emilio/symbols.lst \
[${img_dirs}] \
${trans_tr} ${trans_val};