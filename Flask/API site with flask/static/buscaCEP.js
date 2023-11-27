function buscarCep(novoCep) {
  const contentUrl =  `https://viacep.com.br/ws/${novoCep}/json/`;
  fetch(contentUrl, {
    method: 'GET'
  }).then(response => response.json())
  .then(responseJson => preencherDados(responseJson))
  .catch(error => alert(error));
}
function preencherDados(dadosCep) {
  document.Cadastro.endereco.value = dadosCep.logradouro;
  document.Cadastro.bairro.value = dadosCep.bairro;
  document.Cadastro.cidade.value = dadosCep.localidade;
  document.Cadastro.estado.value = dadosCep.uf;
}

