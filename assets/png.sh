#!/bin/bash

# Verifica se foram fornecidos dois argumentos
if [ "$#" -ne 2 ]; then
    echo "Você deve fornecer exatamente dois argumentos."
    exit 1
fi

# Obtém o diretório onde o script está salvo
script_dir=$(dirname "$0")

# Concatena o diretório do script com o primeiro argumento
in="${script_dir}/$1"

# Concatena o diretório do script com o segundo argumento
out="${script_dir}/$2"

sfdp -x -Goverlap=scale -Tpng $in > $out