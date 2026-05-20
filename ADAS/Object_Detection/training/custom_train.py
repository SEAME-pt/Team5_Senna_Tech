import albumentations as A

from ultralytics.models.yolo.detect import DetectionTrainer


class CustomTrainer(DetectionTrainer):

    def build_dataset(self, img_path, mode="train", batch=None):

        dataset = super().build_dataset(img_path, mode, batch)

        # Apenas augmentations no treino
        if mode == "train":

            dataset.albumentations = A.Compose([

                # --- MOTION BLUR ---
                A.MotionBlur(
                    blur_limit=(3, 7),
                    p=0.30
                ),

                # --- BLUR LEVE ---
                A.GaussianBlur(
                    blur_limit=(3, 5),
                    p=0.10
                ),

                # --- COMPRESSÃO ---
                A.ImageCompression(
                    quality_range=(30, 70),
                    p=0.25
                ),

                # --- ILUMINAÇÃO ---
                A.RandomBrightnessContrast(
                    brightness_limit=0.2,
                    contrast_limit=0.2,
                    p=0.4
                ),

                # --- SOMBRAS ---
                A.RandomShadow(
                    p=0.2
                ),

            ], bbox_params=A.BboxParams(
                format="yolo",
                label_fields=["class_labels"]
            ))

        return dataset
