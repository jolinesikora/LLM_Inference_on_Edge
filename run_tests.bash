cd jetson-containers/

sudo tegrastats --interval 100 --logfile stats_open_llama.txt &
echo "running openlm-research/open_llama_3b_v2"
./run.sh $(./autotag transformers) \
   huggingface-benchmark.py --model=openlm-research/open_llama_3b_v2  > output_open_llama.txt
tegrastats --stop

sudo tegrastats --interval 100 --logfile stats_sheared_llama.txt &
echo "running princeton-nlp/Sheared-LLaMA-2.7B"
./run.sh $(./autotag transformers) \
   huggingface-benchmark.py --model=princeton-nlp/Sheared-LLaMA-2.7B  > output_sheared_llama.txt
tegrastats --stop

sudo tegrastats --interval 100 --logfile stats_gpt.txt &
echo "running gpt"
./run.sh $(./autotag transformers) \
   huggingface-benchmark.py --model=gpt2  > output_gpt.txt
tegrastats --stop