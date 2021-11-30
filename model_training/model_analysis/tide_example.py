import tidecv.datasets as datasets
from tidecv import TIDE


def main():
    gt_path = "../yolov5/output/coco_livestalk-actual.json"
    results_path = "../yolov5/output/coco_livestalk-pred.json"

    gt = datasets.COCO(gt_path)
    results = datasets.COCOResult(results_path)

    tide = TIDE()

    tide.evaluate_range(gt, results, mode=TIDE.BOX)
    tide.summarize()


if __name__ == '__main__':
    main()
