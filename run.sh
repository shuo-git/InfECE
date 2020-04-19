CODE=Path_to_InfECE
TER=Path_to_tercom-0.7.25
ref=Path_to_reference
hyp=Path_to_hypothesis
vocab=Path_to_target_side_vocabulary

echo "Generating TER label..."
python ${CODE}/add_sen_id.py ${ref} ${ref}.ref
python ${CODE}/add_sen_id.py ${hyp} ${hyp}.hyp

java -jar ${TER}/tercom.7.25.jar -r ${ref}.ref -h ${hyp}.hyp -n ${hyp} -s

python ${CODE}/parse_xml.py ${hyp}.xml ${hyp}.shifted
python ${CODE}/shift_back.py ${hyp}.shifted.text ${hyp}.shifted.label ${hyp}.pra

rm ${ref}.ref ${hyp}.hyp ${hyp}.ter ${hyp}.sum ${hyp}.sum_nbest \
    ${hyp}.pra_more ${hyp}.pra ${hyp}.xml ${hyp}.shifted.text \
    ${hyp}.shifted.label 
mv ${hyp}.shifted.text.sb ${hyp}.sb
mv ${hyp}.shifted.label.sb ${hyp}.label


echo "Filtering unaligned tokens..."
for f in ${hyp} ${hyp}.label ${hyp}.conf;do
    if [ ${f} = ${hyp} ]
    then
        python ${CODE}/filter_diff_tok.py ${hyp} ${hyp}.sb ${f}
    else
        python ${CODE}/filter_diff_tok.py ${hyp} ${hyp}.sb ${f} > /dev/null
    fi
done
 

echo "Calculating inference ECE..."
python ${CODE}/calc_ece.py \
    --prob ${hyp}.conf.filt \
    --trans ${hyp}.filt \
    --label ${hyp}.label.filt \
    --vocabulary ${vocab}
