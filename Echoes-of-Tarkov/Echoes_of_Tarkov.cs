using SPTarkov.DI.Annotations;
using SPTarkov.Server.Core.DI;
using SPTarkov.Server.Core.Models.Spt.Mod;
using SPTarkov.Server.Core.Models.Utils;
using System.Reflection;
using WTTServerCommonLib;
using static System.Net.WebRequestMethods;
using Range = SemanticVersioning.Range;

namespace Echoes_of_Tarkov
{
    public record ModMetadata : AbstractModMetadata
    {
        public override string ModGuid { get; init; } = "com.echoesoftarkov.requisitions";
        public override string Name { get; init; } = "Echoes of Tarkov";
        public override string Author { get; init; } = "Pluto!";
        public override SemanticVersioning.Version Version { get; init; } = new("1.0.0");
        public override Range SptVersion { get; init; } = new("~4.0.4");
        public override string License { get; init; } = "MIT";
        public override bool? IsBundleMod { get; init; } = true;
        public override Dictionary<string, Range>? ModDependencies { get; init; } = new()
        {
            { "com.wtt.commonlib", new Range("~2.0.0") }
        };
        public override string? Url { get; init; } = "https://github.com/Reis963/Echoes-of-Tarkov---Requisitions";
        public override List<string>? Contributors { get; init; } = new()
        {
            "Pigeon",
            "ProbablyEukyre",
            "WTT Team",
            "Reis963"
        };
        public override List<string>? Incompatibilities { get; init; }
    }

    [Injectable(TypePriority = OnLoadOrder.PostDBModLoader + 2)]
    public class EchoesOfTarkovMod(WTTServerCommonLib.WTTServerCommonLib wttCommon,
        ISptLogger<EchoesOfTarkovMod> logger) : IOnLoad
    {
        public async Task OnLoad()
        {
            var assembly = Assembly.GetExecutingAssembly();

            await wttCommon.CustomItemServiceExtended.CreateCustomItems(assembly, Path.Join("db", "items"));

            logger.Success("[Echoes of Tarkov] Loaded! | Got something I'm supposed to deliver - yours hand only.");
        }
    }
}
