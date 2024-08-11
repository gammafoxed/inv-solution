namespace addin

open System.Runtime.InteropServices
open Inventor

[<Guid("0665c440-0035-49ba-917e-5b19b04be927")>]
type Server() =
    interface ApplicationAddInServer with
        member this.Activate(_addInSiteObject, _firstTime) = ()
        member this.Deactivate() = ()
        member this.ExecuteCommand _ = ()
        member this.Automation = ()