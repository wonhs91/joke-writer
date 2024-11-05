When installing dependencies for lambda

```
pip install -r ./requirements.txt --platform manylinux_2_17_x86_64 --only-binary=:all: --target ./joke-writer-env/Lib/site-packages --upgrade --no-cache-dir
```
Create zip file
`Compress-Archive .\joke-writer-env\Lib\site-packages\* aws_lambda.zip`
`Compress-Archive .\service\* -Update aws_lambda.zip `