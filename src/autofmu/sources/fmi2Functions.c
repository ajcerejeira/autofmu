#include <string.h>
#include "headers/fmi2Functions.h"

#define GUID "{{ guid }}"
#define NINPUTS {{ inputs|length }}
#define NOUTPUTS {{ outputs|length }}
#define NVARIABLES {{ (inputs + outputs)|length }}

/* Build relationship functions that map the inputs to each output */
{% for output in outputs %}
fmi2Real R_{{ output }}(fmi2Real inputs[], size_t n) {
    return 0.0;
}
{% endfor %}

/* Array of relationship functions that map the inputs to each output*/
fmi2Real (*R[NOUTPUTS])(fmi2Real[], size_t) = {
    {% for output in outputs %}
    R_{{ output }},
    {% endfor %}
};

/* Buffer to save all the model variables */
fmi2Real VARIABLES[NVARIABLES];


/*
 * FMI 2.0 implementation
 */

const char *fmi2GetTypesPlatform()
{
    return fmi2TypesPlatform;
}

const char *fmi2GetVersion()
{
    return fmi2Version;
}

fmi2Status fmi2SetDebugLogging(fmi2Component c,
                               fmi2Boolean loggingOn,
                               size_t nCategories,
                               const fmi2String categories[])
{
    return fmi2OK;
}

fmi2Component fmi2Instantiate(fmi2String instanceName,
                              fmi2Type fmuType,
                              fmi2String fmuGUID,
                              fmi2String fmuResourceLocation,
                              const fmi2CallbackFunctions *functions,
                              fmi2Boolean visible,
                              fmi2Boolean loggingOn)
{
    if (!functions->logger)
    {
        return NULL;
    }

    if (!instanceName || strlen(instanceName) == 0)
    {
        functions->logger(functions->componentEnvironment,
                          "?",
                          fmi2Error,
                          "error",
                          "fmi2Instantiate: Missing instance name.");
        return NULL;
    }

    if (!functions->allocateMemory || !functions->freeMemory)
    {
        functions->logger(functions->componentEnvironment,
                          instanceName,
                          fmi2Error,
                          "error",
                          "fmi2Instantiate: Missing callback function.");
        return NULL;
    }

    if (!fmuGUID || strlen(fmuGUID) == 0)
    {
        functions->logger(functions->componentEnvironment,
                          instanceName,
                          fmi2Error,
                          "error",
                          "fmi2Instantiate: Missing GUID.");
        return NULL;
    }

    if (strcmp(fmuGUID, GUID) != 0)
    {
        functions->logger(functions->componentEnvironment,
                          instanceName,
                          fmi2Error,
                          "error",
                          "fmi2Instantiate: Wrong GUID %s. Expected %s.",
                          fmuGUID,
                          GUID);
        return NULL;
    }

    return (void *)1;
}

void fmi2FreeInstance(fmi2Component c)
{
}

fmi2Status fmi2SetupExperiment(fmi2Component c,
                               fmi2Boolean toleranceDefined,
                               fmi2Real tolerance,
                               fmi2Real startTime,
                               fmi2Boolean stopTimeDefined,
                               fmi2Real stopTime)
{
    return fmi2OK;
}

fmi2Status fmi2EnterInitializationMode(fmi2Component c)
{
    return fmi2OK;
}

fmi2Status fmi2ExitInitializationMode(fmi2Component c)
{
    return fmi2OK;
}

fmi2Status fmi2Terminate(fmi2Component c)
{
    return fmi2OK;
}

fmi2Status fmi2Reset(fmi2Component c)
{
    return fmi2OK;
}

fmi2Status fmi2GetReal(fmi2Component c,
                       const fmi2ValueReference vr[],
                       size_t nvr,
                       fmi2Real value[])
{
    size_t i;
    for (i = 0; i < nvr; i++)
    {
        double (*r)(fmi2Real[], size_t) = R[vr[i]];
        value[i] = r(VARIABLES, NINPUTS);
    }
    return fmi2OK;
}

fmi2Status fmi2GetInteger(fmi2Component c,
                          const fmi2ValueReference vr[],
                          size_t nvr,
                          fmi2Integer value[])
{
    return fmi2OK;
}

fmi2Status fmi2GetBoolean(fmi2Component c,
                          const fmi2ValueReference vr[],
                          size_t nvr,
                          fmi2Boolean value[])
{
    return fmi2OK;
}

fmi2Status fmi2GetString(fmi2Component c,
                         const fmi2ValueReference vr[],
                         size_t nvr,
                         fmi2String value[])
{
    return fmi2OK;
}

fmi2Status fmi2SetReal(fmi2Component c,
                       const fmi2ValueReference vr[],
                       size_t nvr,
                       const fmi2Real value[])
{
    size_t i;
    for (i = 0; i < nvr; i++)
    {
        VARIABLES[vr[i]] = value[i];
    }
    return fmi2OK;
}

fmi2Status fmi2SetInteger(fmi2Component c,
                          const fmi2ValueReference vr[],
                          size_t nvr,
                          const fmi2Integer value[])
{
    return fmi2OK;
}

fmi2Status fmi2SetBoolean(fmi2Component c,
                          const fmi2ValueReference vr[],
                          size_t nvr,
                          const fmi2Boolean value[])
{
    return fmi2OK;
}

fmi2Status fmi2SetString(fmi2Component c,
                         const fmi2ValueReference vr[],
                         size_t nvr,
                         const fmi2String value[])
{
    return fmi2OK;
}

fmi2Status fmi2GetFMUstate(fmi2Component c,
                           fmi2FMUstate *FMUstate)
{
    return fmi2OK;
}

fmi2Status fmi2SetFMUstate(fmi2Component c,
                           fmi2FMUstate FMUstate)
{
    return fmi2OK;
}

fmi2Status fmi2FreeFMUstate(fmi2Component c,
                            fmi2FMUstate *FMUstate)
{
    return fmi2OK;
}

fmi2Status fmi2SerializedFMUstateSize(fmi2Component c,
                                      fmi2FMUstate FMUstate,
                                      size_t *size)
{
    return fmi2OK;
}

fmi2Status fmi2SerializeFMUstate(fmi2Component c,
                                 fmi2FMUstate FMUstate,
                                 fmi2Byte serializedState[],
                                 size_t size)
{
    return fmi2OK;
}

fmi2Status fmi2DeSerializeFMUstate(fmi2Component c,
                                   const fmi2Byte serializedState[],
                                   size_t size,
                                   fmi2FMUstate *FMUstate)
{
    return fmi2OK;
}

fmi2Status fmi2GetDirectionalDerivative(fmi2Component c,
                                        const fmi2ValueReference vUnknown_ref[],
                                        size_t nUnknown,
                                        const fmi2ValueReference vKnown_ref[],
                                        size_t nKnown,
                                        const fmi2Real dvKnown[],
                                        fmi2Real dvUnknown[])
{
    return fmi2OK;
}

fmi2Status fmi2SetRealInputDerivatives(fmi2Component c,
                                       const fmi2ValueReference vr[],
                                       size_t nvr,
                                       const fmi2Integer order[],
                                       const fmi2Real value[])
{
    return fmi2OK;
}

fmi2Status fmi2GetRealOutputDerivatives(fmi2Component c,
                                        const fmi2ValueReference vr[],
                                        size_t nvr,
                                        const fmi2Integer order[],
                                        fmi2Real value[])
{
    return fmi2OK;
}

fmi2Status fmi2DoStep(fmi2Component c,
                      fmi2Real currentCommunicationPoint,
                      fmi2Real communicationStepSize,
                      fmi2Boolean noSetFMUStatePriorToCurrentPoint)
{
    return fmi2OK;
}

fmi2Status fmi2CancelStep(fmi2Component c)
{
    return fmi2OK;
}

fmi2Status fmi2GetStatus(fmi2Component c,
                         const fmi2StatusKind s,
                         fmi2Status *value)
{
    return fmi2OK;
}

fmi2Status fmi2GetRealStatus(fmi2Component c,
                             const fmi2StatusKind s,
                             fmi2Real *value)
{
    return fmi2OK;
}

fmi2Status fmi2GetIntegerStatus(fmi2Component c,
                                const fmi2StatusKind s,
                                fmi2Integer *value)
{
    return fmi2OK;
}

fmi2Status fmi2GetBooleanStatus(fmi2Component c,
                                const fmi2StatusKind s,
                                fmi2Boolean *value)
{
    return fmi2OK;
}

fmi2Status fmi2GetStringStatus(fmi2Component c,
                               const fmi2StatusKind s,
                               fmi2String *value)
{
    return fmi2OK;
}