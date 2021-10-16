# Estima_Temp_Agua_com_Temp_Ar
Métodos de regressão para a estimação da temperatura da água usando a média móvel da temperatura do ar.

As rotinas faz parte do Toolkit SABIA, criado dentro do projeto Iguaçu - Estudos de bacias hidrográficas
- https://github.com/UFPR-PPGERHA/Projeto_iguacu
- https://github.com/UFPR-PPGERHA/SABIA

Os dados utilizados como exemplo são da bacia do rio Iguaçu, gerada com as rotinas do projeto Iguaçu
- https://drive.google.com/drive/folders/1dtha0Mtp30yqa4HXv4SlkT7UDSMYaFBV?usp=sharing
- https://drive.google.com/drive/folders/1cEu2csxzwmJpK2e2Kn_xvkAqQbnz8sJH?usp=sharing
 
A ideia foi baseada nos resultados obtidos na dissertação da Geovana Thais Colombo: 
 - "Dinâmica térmica em rios e relações com variáveis meteorológicas" 
 - https://acervodigital.ufpr.br/handle/1884/63819

EXEMPLOS
# Melhores Reusultados usando R2 como métrica de seleção
![R2_geral](https://user-images.githubusercontent.com/73908748/131568897-cd062732-1ca8-45d8-a8a5-75e0407225ee.png)

# Serie Temporal ajusta para a estação 65004900 - Usando a métrica MAE como base de seleção do método de regressão
![Time_series_MAE_65004900](https://user-images.githubusercontent.com/73908748/131569047-8cff5bb2-e8fe-40ca-ae97-3ce3946f3bee.png)
