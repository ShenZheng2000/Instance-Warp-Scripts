function run_tide() {
    TASK=$1
    echo "TASK is $TASK"
    FILE1="/home/aghosh/Projects/2PCNet/outputs/$TASK/inference/coco_instances_results.json"
    FILE2="/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_night.json"

    if [ -f "$FILE1" ] && [ -f "$FILE2" ]; then
        python tide.py "$FILE1" "$FILE2"
    else
        echo "Files do not exist."
    fi
}


run_tide 'pretrained'