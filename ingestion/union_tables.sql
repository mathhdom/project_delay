WITH obra AS(
    SELECT *
    FROM modulo_empreendimento_obra
),

mod_eq_sub AS(
    SELECT IdeMdl, DscTipEqp, NumFasMdlEqp, 
    MdaCpeRaiNegMdlEqp, MdaCpeRaivPosMdlEqp, 
    DscFinMdlEqp, DscIdcExsMdlCnr, MdaPotAtvMdlEqp, MdaTnsScdMdlEqp,
    MdaTnsTiaMdlEqp, NomSubestacao AS NomSubestacaoEqp, NomLongoSubestacao AS 
    NomLongoSubestacaoEqp, 
    SigUFSubestacao AS SigUFSubestacaoEqp
    FROM modulo_equipamento_subestacao
),

mod_man_sub AS(
    SELECT IdeMdl, SglTipAnj, DscTipAnj,
    IdcTipMdlMno, DscMdlMno, QtdDijMdlMno, QtdChvSccMdlMno,
    NomSubestacao AS NomSubestacaoAnj, NomLongoSubestacao AS
    NomLongoSubestacaoAnj, SigUFSubestacao AS SigUFSubestacaoAnj
    FROM modulo_manobra_subestacao_tipo_arranjo
),

mod_lt AS(
    SELECT IdeMdl, DscSitLinTms, NumCcuLinTms, QtdTorLinTms,
    NumEtnLinTms, NomSubestacaoOrigem, NomLongoSubestacaoOrigem, 
    SigUFSubestacaoOrigem, NomSubestacaoDestino, 
    NomLongoSubestacaoDestino, SigUFSubestacaoDestino
    FROM modulo_linha_transmissao
),

mod_ger_sub AS(
    SELECT IdeMdl, IdcPrtMdlGrl,
    SglTipAnj AS SglTipAnjGer, DscTipAnj AS DscTipAnjGer, 
    NomSubestacao AS NomSubestacaoGer, NomLongoSubestacao AS
    NomLongoSubestacaoGer, SigUFSubestacao AS SigUFSubestacaoGer
    FROM modulo_geral_subestacao_tipo_arranjo
),

total AS(

SELECT * 
FROM obra as t1

LEFT JOIN mod_eq_sub AS t2
ON t1.IdeMdl = t2.IdeMdl

LEFT JOIN mod_man_sub AS t3
ON t1.IdeMdl = t3.IdeMdl

LEFT JOIN mod_lt AS t4
ON t1.IdeMdl = t4.IdeMdl

LEFT JOIN mod_ger_sub as t5
ON t1.IdeMdl = t5.IdeMdl
)

SELECT DatGeracaoConjuntoDados, IdeOnsEpd, NomEpd, DscEpd, DscSituacaoEpd,
DatEfeOprComEpd, DatCaoCgmAtoLgl, DatOprComEpd, DscObr, DscSitObr, NumVdaUtlMdl,
DatOprComObr, DscTipObr, IdeMdl, IdeOnsMdl, NomMdl, DscMdl, IdeTipMdl, DscSituacaoModulo,
DscTipMdl, SigTipMdl, DscClfMdl, SglClfMdl, DscItmClfMdl, IdeCcoTarReceita,
VlrHisRct, DatFimCcd, 
DscTipEqp, NumFasMdlEqp, 
MdaCpeRaiNegMdlEqp, MdaCpeRaivPosMdlEqp, 
DscFinMdlEqp, DscIdcExsMdlCnr, MdaPotAtvMdlEqp, MdaTnsScdMdlEqp,
MdaTnsTiaMdlEqp,
SglTipAnj, DscTipAnj,
IdcTipMdlMno, DscMdlMno, QtdDijMdlMno, QtdChvSccMdlMno,
DscSitLinTms, NumCcuLinTms, QtdTorLinTms, NumEtnLinTms,
IdcPrtMdlGrl, SglTipAnjGer, DscTipAnjGer,
COALESCE(
    NomSubestacaoGer,
    NomSubestacaoDestino,
    NomSubestacaoAnj,
    NomSubestacaoEqp
) AS NomSubestacao,
COALESCE(
    NomLongoSubestacaoGer,
    NomLongoSubestacaoDestino,
    NomLongoSubestacaoAnj,
    NomLongoSubestacaoEqp
) AS NomLongoSubestacao,
COALESCE(
    SigUFSubestacaoGer,
    SigUFSubestacaoDestino,
    SigUFSubestacaoAnj,
    SigUFSubestacaoEqp
) AS SigUFSubestacao
FROM total

